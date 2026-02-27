const openBtn = document.querySelector(".open_sidebar");
const closeBtn = document.querySelector(".close_sidebar");
const sidebar = document.querySelector(".sidebar");
const add_comment_model = document.querySelector(".add-comment-btn");


if (openBtn && closeBtn && sidebar) {

  openBtn.addEventListener("click", () => {
    sidebar.classList.add("open");
  });

  closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("open");
  });

}




// Toggle Comments - Show/Hide all comments
function toggleComments(taskId) {
  const commentsContainer = document.getElementById('comments-' + taskId);
  const btn = commentsContainer.closest('.task-comments-section').querySelector('.view-all-comments-btn');
  const hiddenComments = commentsContainer.querySelectorAll('.comment-item.hidden-comment');
  const viewText = btn.querySelector('.view-text');
  const hideText = btn.querySelector('.hide-text');
  
  const isExpanded = btn.classList.contains('expanded');
  
  if (isExpanded) {
    // Hide comments
    hiddenComments.forEach(comment => {
      comment.style.display = 'none';
    });
    btn.classList.remove('expanded');
    viewText.style.display = 'inline';
    hideText.style.display = 'none';
  } else {
    // Show all comments
    hiddenComments.forEach(comment => {
      comment.style.display = 'flex';
    });
    btn.classList.add('expanded');
    viewText.style.display = 'none';
    hideText.style.display = 'inline';
  }
}
// Comment Modal Logic
const commentModal = document.querySelector(".add_comment_model");
const closeModalBtns = document.querySelectorAll(".close-modal-btn");
const commentForm = document.getElementById("comment-form");
const parentCommentInput = document.getElementById("parent_comment_id");

function openCommentModal(parentId = null) {
    if (!commentModal) return;
    console.log("Opening comment modal");
    
    // Set parent comment id for replies
    if (parentCommentInput) {
        parentCommentInput.value = parentId || "";
    }
    
    // Update modal title for replies
    const modalTitle = commentModal.querySelector(".comment-modal-header h2");
    if (modalTitle) {
        modalTitle.textContent = parentId ? "💬 Reply to Comment" : "💬 Add New Comment";
    }
    
    commentModal.classList.add("open");
    document.body.style.overflow = "hidden"; // Prevent background scroll
}

function closeCommentModal() {
    if (!commentModal) return;
    console.log("Closing comment modal");
    
    commentModal.classList.remove("open");
    document.body.style.overflow = ""; // Restore scroll
    
    // Clear form
    if (commentForm) {
        commentForm.reset();
    }
    if (parentCommentInput) {
        parentCommentInput.value = "";
    }
}

// Open modal on button click
if (add_comment_model) {
    add_comment_model.addEventListener("click", function() {
        openCommentModal();
    });
}

// Close modal buttons
if (closeModalBtns) {
    closeModalBtns.forEach(btn => {
        btn.addEventListener("click", closeCommentModal);
    });
}

// Close modal on outside click
if (commentModal) {
    commentModal.addEventListener("click", function(e) {
        if (e.target === commentModal) {
            closeCommentModal();
        }
    });
}

// Close modal on Escape key
document.addEventListener("keydown", function(e) {
    if (e.key === "Escape" && commentModal && commentModal.classList.contains("open")) {
        closeCommentModal();
    }
});

// Reply button function (called from HTML onclick)
function replyToComment(commentId) {
    openCommentModal(commentId);
}