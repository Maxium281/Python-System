// js/enhanced-interactions.js - 增强交互效果
document.addEventListener("DOMContentLoaded", function () {
  // 1. 平滑滚动效果
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: "smooth",
        });
      }
    });
  });

  // 2. 增强选项交互
  const optionItems = document.querySelectorAll(".list-group-item");
  optionItems.forEach((item) => {
    const radio = item.querySelector('input[type="radio"]');
    const checkbox = item.querySelector('input[type="checkbox"]');
    const input = radio || checkbox;

    if (input) {
      // 点击整个选项区域选择
      item.addEventListener("click", function (e) {
        if (e.target === input) return; // 防止重复触发

        if (radio) {
          // 单选：取消所有其他选项
          document
            .querySelectorAll(`input[name="${radio.name}"]`)
            .forEach((r) => {
              r.checked = false;
              r.closest(".list-group-item")?.classList.remove("active");
            });
        }

        input.checked = !input.checked;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      });

      // 同步选中状态和样式
      input.addEventListener("change", function () {
        if (this.checked) {
          item.classList.add("active");

          // 添加选中动画
          const checkmark = document.createElement("span");
          checkmark.className = "checkmark";
          checkmark.innerHTML = "✓";
          checkmark.style.cssText = `
            position: absolute;
            right: 15px;
            background: var(--primary-gradient);
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            animation: popIn 0.3s ease-out;
          `;

          // 移除旧的checkmark
          const oldCheckmark = item.querySelector(".checkmark");
          if (oldCheckmark) oldCheckmark.remove();

          item.style.position = "relative";
          item.appendChild(checkmark);
        } else {
          item.classList.remove("active");
          const checkmark = item.querySelector(".checkmark");
          if (checkmark) checkmark.remove();
        }
      });
    }
  });

  // 3. 按钮波纹效果
  const buttons = document.querySelectorAll(".btn");
  buttons.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const ripple = document.createElement("span");
      ripple.style.cssText = `
        position: absolute;
        background: rgba(255, 255, 255, 0.4);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        width: 100px;
        height: 100px;
        left: ${x - 50}px;
        top: ${y - 50}px;
        pointer-events: none;
      `;

      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

  // 4. 卡片悬停效果增强
  const cards = document.querySelectorAll(".card:not(.text-center)");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-10px)";
      this.style.boxShadow = "0 20px 50px rgba(0, 0, 0, 0.15)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(-8px)";
      this.style.boxShadow = "var(--shadow-hover)";
    });
  });

  // 5. 收藏按钮特效
  const collectBtns = document.querySelectorAll("#collectBtn, .collect-btn");
  collectBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const isCollected = this.classList.contains("btn-warning");
      const icon = this.querySelector("i");

      if (isCollected) {
        this.className = "btn btn-outline-warning";
        this.innerHTML = '<i class="fa fa-star"></i> 收藏题目';

        // 取消收藏动画
        icon.style.animation = "starOut 0.5s ease-out";
      } else {
        this.className = "btn btn-warning";
        this.innerHTML = '<i class="fa fa-star"></i> 已收藏';

        // 收藏动画
        icon.style.animation = "starIn 0.5s ease-out";

        // 添加浮动效果
        this.style.transform = "scale(1.1)";
        setTimeout(() => {
          this.style.transform = "scale(1)";
        }, 300);
      }

      setTimeout(() => {
        icon.style.animation = "";
      }, 500);
    });
  });

  // 6. 进度条动画
  const progressBars = document.querySelectorAll(".progress-bar");
  progressBars.forEach((bar) => {
    const width = bar.style.width || getComputedStyle(bar).width;
    bar.style.width = "0%";

    setTimeout(() => {
      bar.style.transition = "width 1.5s ease-in-out";
      bar.style.width = width;
    }, 300);
  });

  // 7. 表单提交反馈
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> 处理中...';
        submitBtn.disabled = true;

        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }, 1500);
      }
    });
  });

  // 8. 页面加载动画
  const cardsToAnimate = document.querySelectorAll(
    ".card, .alert, .list-group"
  );
  cardsToAnimate.forEach((el, index) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";

    setTimeout(() => {
      el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    }, 100 * index);
  });
});

// 添加CSS动画关键帧
const style = document.createElement("style");
style.textContent = `
  @keyframes ripple-animation {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }
  
  @keyframes starIn {
    0% { transform: scale(0.5) rotate(0deg); opacity: 0; }
    50% { transform: scale(1.2) rotate(180deg); opacity: 1; }
    100% { transform: scale(1) rotate(360deg); opacity: 1; }
  }
  
  @keyframes starOut {
    0% { transform: scale(1) rotate(0deg); opacity: 1; }
    100% { transform: scale(0.5) rotate(-180deg); opacity: 0; }
  }
  
  @keyframes popIn {
    0% { transform: scale(0); opacity: 0; }
    70% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
  }
`;
document.head.appendChild(style);
