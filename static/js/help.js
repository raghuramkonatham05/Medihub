document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("helpSearch");
const faqLinks = document.querySelectorAll(".faq-list a");

searchInput.addEventListener("input", () => {
  const value = searchInput.value.toLowerCase();

  faqLinks.forEach(link => {
    const text = link.dataset.title.toLowerCase();
    link.parentElement.style.display =
      text.includes(value) ? "block" : "none";
  });
});

});
function submitFeedback(response) {
  const feedbackBox = document.getElementById("feedbackBox");

  if (!feedbackBox) return;

  feedbackBox.innerHTML = `
    <h3>Thank you for your feedback!</h3>
    <p style="margin-top: 12px; font-size: 16px; color: #475569;">
      Your response helps us improve MediHub support articles.
    </p>
  `;
}
