"use strict";

window.addEventListener('click', (e) => {
	const btn = e.target.closest('button'), modal = e.target.closest('dialog');

	if (modal) {
		if (e.target.tagName === 'DIALOG') modal.close();
		else if (btn.getAttribute('data-modal-btn') !== null) modal.close();
	}
	else if (btn) {
		const dataModal = btn.getAttribute('data-modal');

		if (dataModal) {
			const modal = document.getElementById(dataModal);
			modal.showModal();
		}
	}
})