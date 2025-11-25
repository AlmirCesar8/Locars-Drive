import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
import { getFirestore, doc, setDoc, updateDoc, onSnapshot, collection, query, where, writeBatch, Timestamp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

// --- Configurações Iniciais do Firebase (MANDATÓRIO) ---
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

// Inicializa o Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

let currentUserId = null;

// Referências DOM
const loadingIndicator = document.getElementById('loading-indicator');
const notificationsList = document.getElementById('notifications-list');
const noNotificationsMessage = document.getElementById('no-notifications');
const userIdDisplay = document.getElementById('user-id-display');
const markAllReadBtn = document.getElementById('mark-all-read-btn');

// --- Funções Auxiliares ---

/**
 * Converte um objeto de notificação do Firestore para um objeto renderizável.
 * @param {Object} docData - Dados do documento.
 * @param {string} docId - ID do documento.
 * @returns {Object} Notificação formatada.
 */
function formatNotification(docData, docId) {
    // Garante que a data seja um objeto Date ou null
    const date = docData.data_criacao instanceof Timestamp ? docData.data_criacao.toDate() : null;
    
    // Define o ícone com base no tipo
    let icon = '🔔'; // Padrão
    let iconColorClass = 'text-blue-500'; // Cor padrão (info)

    switch (docData.tipo) {
        case 'alerta':
            icon = '🚨';
            iconColorClass = 'text-red-500';
            break;
        case 'sucesso':
            icon = '✅';
            iconColorClass = 'text-green-500';
            break;
        case 'sistema':
            icon = '⚙️';
            iconColorClass = 'text-gray-500';
            break;
        case 'locacao':
            icon = '🚗';
            iconColorClass = 'text-yellow-600';
            break;
    }

    return {
        id: docId,
        titulo: docData.titulo || 'Notificação sem Título',
        mensagem: docData.mensagem || 'Nenhuma mensagem.',
        data_formatada: date ? date.toLocaleString('pt-BR') : 'Data Indisponível',
        lida: docData.lida || false,
        tipo: docData.tipo || 'info',
        icon: icon,
        iconColorClass: iconColorClass
    };
}

/**
 * Cria o elemento HTML de uma única notificação.
 * @param {Object} notification - Objeto de notificação formatado.
 * @returns {string} HTML do item.
 */
function createNotificationItem(notification) {
    const readClass = notification.lida ? 'notification-read' : 'notification-unread';
    const isUnread = !notification.lida;

    // Use o ID da notificação para a função de marcação individual
    const markAsReadHtml = isUnread 
        ? `<button onclick="marcarNotificacaoLida('${notification.id}')" 
                   class="text-xs text-indigo-600 hover:text-indigo-800 font-medium">
                   Marcar como Lida
           </button>`
        : '';

    return `
        <div id="notif-${notification.id}" class="notification-item ${readClass}">
            <div class="notification-content">
                <div class="icon ${notification.iconColorClass}">${notification.icon}</div>
                <div>
                    <p class="title">${notification.titulo}</p>
                    <p class="text-sm">${notification.mensagem}</p>
                    <span class="notification-timestamp">${notification.data_formatada}</span>
                </div>
            </div>
            <div class="notification-actions">
                ${markAsReadHtml}
            </div>
        </div>
    `;
}

/**
 * Renderiza a lista de notificações e atualiza o contador.
 * @param {Array<Object>} notifications - Lista de notificações do Firestore.
 */
function renderNotifications(notifications) {
    const sortedNotifications = notifications.sort((a, b) => {
        // Ordena: não lidas primeiro, depois por data decrescente
        if (a.lida !== b.lida) {
            return a.lida ? 1 : -1;
        }
        // Assumindo que data_criacao é um objeto Date ou Timestamp
        const dateA = a.data_criacao?.toDate?.() || 0;
        const dateB = b.data_criacao?.toDate?.() || 0;
        return dateB - dateA; 
    }).map(doc => formatNotification(doc, doc.id));

    
    notificationsList.innerHTML = sortedNotifications.map(createNotificationItem).join('');
    
    const unreadCount = sortedNotifications.filter(n => !n.lida).length;
    
    markAllReadBtn.innerHTML = `Marcar ${unreadCount} como Lidas`;
    markAllReadBtn.disabled = unreadCount === 0;
    
    loadingIndicator.style.display = 'none';
    noNotificationsMessage.style.display = sortedNotifications.length === 0 ? 'block' : 'none';
    notificationsList.style.display = sortedNotifications.length > 0 ? 'flex' : 'none';
}

/**
 * Marca uma única notificação como lida no Firestore.
 * @param {string} notificationId - ID da notificação.
 */
window.marcarNotificacaoLida = async (notificationId) => {
    if (!currentUserId) return;

    try {
        const notifDocRef = doc(db, 'artifacts', appId, 'users', currentUserId, 'notificacoes', notificationId);
        await updateDoc(notifDocRef, {
            lida: true
        });
        console.log(`Notificação ${notificationId} marcada como lida.`);
    } catch (error) {
        console.error("Erro ao marcar notificação como lida:", error);
    }
};


/**
 * Marca TODAS as notificações não lidas como lidas.
 */
window.marcarTodasLidas = async () => {
    if (!currentUserId) return;

    markAllReadBtn.disabled = true; // Desabilita para evitar cliques duplos

    try {
        // Cria uma consulta para buscar todas as notificações não lidas
        const notificationsRef = collection(db, 'artifacts', appId, 'users', currentUserId, 'notificacoes');
        const q = query(notificationsRef, where('lida', '==', false));
        const snapshot = await getDocs(q);

        if (snapshot.empty) {
            console.log("Nenhuma notificação não lida para marcar.");
            return;
        }

        const batch = writeBatch(db);
        snapshot.forEach((doc) => {
            batch.update(doc.ref, {
                lida: true
            });
        });

        await batch.commit();
        console.log(`Marcadas ${snapshot.size} notificações como lidas.`);

    } catch (error) {
        console.error("Erro ao marcar todas como lidas:", error);
        // O re-habilita se houver falha
    } finally {
        // A UI será atualizada automaticamente via onSnapshot
    }
};

/**
 * Ouve o estado de autenticação e inicia a busca de dados.
 */
onAuthStateChanged(auth, async (user) => {
    if (user) {
        currentUserId = user.uid;
        userIdDisplay.textContent = currentUserId;
        
        // 1. Defina a coleção de notificações para o usuário atual
        const notificationsRef = collection(db, 'artifacts', appId, 'users', currentUserId, 'notificacoes');
        
        // 2. Cria a query, ordenando por data de criação (exemplo: 'data_criacao')
        // OBS: Evitar orderBy no Canvas, mas para fins didáticos, se data_criacao existe, use.
        // Se der erro de index, remova o orderBy e ordene em JS (como já está na renderNotifications)
        // const q = query(notificationsRef, orderBy('data_criacao', 'desc'));

        // 3. Ouve as mudanças em tempo real (onSnapshot)
        onSnapshot(notificationsRef, (snapshot) => {
            const notifications = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
            renderNotifications(notifications);
        }, (error) => {
            console.error("Erro ao receber notificações em tempo real:", error);
            loadingIndicator.textContent = "Erro ao carregar notificações. Verifique o console.";
        });

    } else {
        // Tenta autenticar anonimamente se não houver token customizado
        try {
            if (initialAuthToken) {
                await signInWithCustomToken(auth, initialAuthToken);
            } else {
                await signInAnonymously(auth);
            }
        } catch (error) {
            console.error("Erro na autenticação:", error);
            loadingIndicator.textContent = "Erro de autenticação. Tente recarregar.";
        }
    }
});

// A UI é renderizada dentro do onAuthStateChanged, garantindo que o currentUserId esteja pronto.