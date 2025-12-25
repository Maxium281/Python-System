# -*- coding: utf-8 -*-
// js/animations.js - 交互动画效果
document.addEventListener("DOMContentLoaded", function () {
  // 选项选择效果
  const optionItems = document.querySelectorAll(".list-group-item");
  optionItems.forEach((item) => {
    item.addEventListener("click", function () {
      // 移除其他选项的选中样式
      const parent = this.closest(".list-group");
      if (parent) {
        parent.querySelectorAll(".list-group-item").forEach((el) => {
          el.classList.remove("active", "border-primary");
        });
      }

      // 添加当前选项的选中样式
      this.classList.add("active", "border-primary");

      // 如果是单选题，自动选中对应的radio/checkbox
      const input = this.querySelector("input");
      if (input) {
        input.checked = true;

        // 触发自定义事件
        const event = new Event("change", { bubbles: true });
        input.dispatchEvent(event);
      }
    });
  });

  // 按钮悬停效果
  const buttons = document.querySelectorAll(".btn");
  buttons.forEach((btn) => {
    btn.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-3px)";
    });

    btn.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });

  // 卡片悬停效果
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.boxShadow = "0 15px 40px rgba(0, 0, 0, 0.12)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.08)";
    });
  });

  // 页面滚动动画
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate__animated", "animate__fadeInUp");
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // 观察需要动画的元素
  document.querySelectorAll(".card, .alert, .list-group-item").forEach((el) => {
    observer.observe(el);
  });
});
