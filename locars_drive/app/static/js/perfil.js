// static/js/perfil.js
document.addEventListener("DOMContentLoaded", () => {

  /* ---------- Modal Reutilizável ---------- */
  const confirmModal = document.getElementById('confirm-modal');
  const confirmTitle = document.getElementById('confirm-title');
  const confirmText = document.getElementById('confirm-text');
  const btnCancel = document.getElementById('confirm-cancel');
  const btnAccept = document.getElementById('confirm-accept');
  let confirmResolve = null;

  function openConfirm(text) {
    confirmText.textContent = text || 'Tem certeza?';
    confirmModal.style.display = 'flex';
    confirmModal.setAttribute('aria-hidden','false');
    return new Promise((resolve) => {
      confirmResolve = resolve;
    });
  }

  function closeConfirm() {
    confirmModal.style.display = 'none';
    confirmModal.setAttribute('aria-hidden','true');
    if (confirmResolve) confirmResolve(false);
    confirmResolve = null;
  }

  btnCancel?.addEventListener('click', () => {
    if (confirmResolve) confirmResolve(false);
    closeConfirm();
  });

  btnAccept?.addEventListener('click', () => {
    if (confirmResolve) confirmResolve(true);
    closeConfirm();
  });

  /* intercepta botões com data-confirm */
  /* intercepta botões e links com data-confirm */
document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', async (e) => {
        e.preventDefault(); // Impede a ação padrão (navegação ou submissão)
        
        const text = el.getAttribute('data-confirm') || 'Deseja confirmar?';
        const ok = await openConfirm(text);
        if (!ok) return;

        // --- LÓGICA DE AÇÃO CORRIGIDA: Trata Links (Logout) e Forms (Salvar) ---
        
        // 1. Se o elemento for um LINK (<a>), navegue para o HREF
        if (el.tagName === 'A') {
            window.location.href = el.getAttribute('href');
            return;
        }

        // 2. Se for um botão dentro de um FORM, submete o form
        const insideForm = el.closest('form');
        if (insideForm) {
            insideForm.submit();
            return;
        }

        // 3. Se tiver data-action (para ações customizadas)
        const action = el.getAttribute('data-action');
        if (action) {
            // acionar ações customizadas: remove-card, set-default, cancel-plan etc.
            const customEvent = new CustomEvent('perfil:action', { detail: { action, element: el } });
            document.dispatchEvent(customEvent);
        }
    });
});
// (Restante do seu código JS permanece inalterado)

  /* ---------- Edit inline para perfil_info ---------- */
  function enableInlineEditor(containerSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return;
    container.querySelectorAll('.btn-edit').forEach(btn => {
      btn.addEventListener('click', () => {
        const card = btn.closest('.card');
        card.querySelectorAll('input,select,textarea').forEach(f => f.removeAttribute('readonly'));
        card.classList.add('editing');
        // mostrar botões salvar/cancel
        const save = card.querySelector('.btn-save');
        const cancel = card.querySelector('.btn-cancel');
        if (save) save.style.display = 'inline-block';
        if (cancel) cancel.style.display = 'inline-block';
      });
    });

    container.querySelectorAll('.btn-cancel').forEach(btn => {
      btn.addEventListener('click', () => {
        const card = btn.closest('.card');
        // recarregar página para cancelar (simplest way) — ou você pode resetar campos via JS
        location.reload();
      });
    });

    container.querySelectorAll('.btn-save').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const text = btn.getAttribute('data-confirm') || 'Salvar alterações?';
        const ok = await openConfirm(text);
        if (!ok) return;
        const form = btn.closest('form');
        if (form) form.submit();
      });
    });
  }
  enableInlineEditor('.perfil-content');

  /* ---------- Avatar edit + preview ---------- */
  const avatarContainer = document.getElementById('avatar-container');
  const avatarEditBtn = document.getElementById('avatar-edit-btn');
  const avatarFile = document.getElementById('avatar-file');
  const btnSelectAvatar = document.getElementById('btn-select-avatar');
  const avatarFilename = document.getElementById('avatar-filename');
  const avatarPreviewBox = document.getElementById('avatar-preview');
  const previewImg = document.getElementById('preview-img');
  const btnSaveAvatar = document.getElementById('btn-save-avatar');

  if (btnSelectAvatar && avatarFile) {
    btnSelectAvatar.addEventListener('click', () => avatarFile.click());
    avatarFile.addEventListener('change', () => {
      const f = avatarFile.files[0];
      if (!f) {
        avatarFilename.textContent = '';
        avatarPreviewBox.style.display = 'none';
        return;
      }
      avatarFilename.textContent = f.name;
      const reader = new FileReader();
      reader.onload = e => {
        previewImg.src = e.target.result;
        avatarPreviewBox.style.display = 'block';
      };
      reader.readAsDataURL(f);
    });
  }

  /* Se existir o botão salvar avatar, usar modal flow */
  if (btnSaveAvatar) {
    btnSaveAvatar.addEventListener('click', async (e) => {
      e.preventDefault();
      const ok = await openConfirm(btnSaveAvatar.getAttribute('data-confirm') || 'Salvar imagem?');
      if (!ok) return;
      const form = document.getElementById('form-avatar');
      if (form) form.submit();
    });
  }

  /* ---------- actions customas (cartões, cancelar plano, etc) ---------- */
  document.addEventListener('perfil:action', (ev) => {
    const { action, element } = ev.detail;
    if (action === 'remove-card') {
      // exemplo: enviar fetch para /remover-cartao (backend)
      // Aqui apenas exibe console — integrar depois
      console.log('Remover cartão id=', element.dataset.cardId);
      // opcional: submeter form oculto
    } else if (action === 'set-default') {
      console.log('Definir padrão id=', element.dataset.cardId);
    } else if (action === 'cancel-plan') {
      console.log('Cancelar plano');
    }
  });

  /* ---------- esconder/mostrar CNH na edição (reuso) ---------- */
  const radiosCNH = document.querySelectorAll("input[name='tem_cnh']");
  const campoCNH = document.getElementById("cnh_campo_wrapper") || document.getElementById("campo-cnh");
  if (radiosCNH.length && campoCNH) {
    function toggleCNH(){ 
      const sel = document.querySelector("input[name='tem_cnh']:checked")?.value;
      if (sel === 'sim') campoCNH.style.display = 'block';
      else campoCNH.style.display = 'none';
    }
    radiosCNH.forEach(r => r.addEventListener('change', toggleCNH));
    toggleCNH();
  }

  /* ---------- fechar modal com ESC ---------- */
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && confirmModal && confirmModal.style.display === 'flex') closeConfirm();
  });

});

