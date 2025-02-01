function toggleDetails(element) {
  const details = element.nextElementSibling;
  if (details.style.display === "none" || details.style.display === "") {
      details.style.display = "flex";
      details.style.height = "300px"; // Установить высоту
  } else {
      details.style.display = "none";
      details.style.height = "0";
  }
}



document.querySelector(".jsFilter").addEventListener("click", function () {
    document.querySelector(".filter-menu").classList.toggle("active");
  });
  
  document.querySelector(".grid").addEventListener("click", function () {
    document.querySelector(".list").classList.remove("active");
    document.querySelector(".grid").classList.add("active");
    document.querySelector(".products-area-wrapper").classList.add("gridView");
    document
      .querySelector(".products-area-wrapper")
      .classList.remove("tableView");
  });
  
  document.querySelector(".list").addEventListener("click", function () {
    document.querySelector(".list").classList.add("active");
    document.querySelector(".grid").classList.remove("active");
    document.querySelector(".products-area-wrapper").classList.remove("gridView");
    document.querySelector(".products-area-wrapper").classList.add("tableView");
  });
  
  document.addEventListener('DOMContentLoaded', function () {
    var modeSwitch = document.querySelector('.mode-switch');
    if (modeSwitch) {
      modeSwitch.addEventListener('click', function () {
        document.documentElement.classList.toggle('light');
        modeSwitch.classList.toggle('active');
      });
    }
  });


// для план/факта выделяет цветом
document.addEventListener("DOMContentLoaded", () => {
  const productCells = document.querySelectorAll(".product-cell");

  productCells.forEach(cell => {
      const factSpan = cell.querySelector(".fact");
      const planSpan = cell.querySelector(".plan");

      // Проверяем наличие элементов
      if (!factSpan || !planSpan) {
          console.warn("Не удалось найти один из span в:", cell);
          return; // Прерываем текущую итерацию, если элементы не найдены
      }

      const factValue = parseFloat(factSpan.textContent);
      const planValue = parseFloat(planSpan.textContent);

      console.log(factValue, planValue); // Проверка значений

      // Сравниваем значения
      if (factValue < planValue) {
          factSpan.classList.add("highlight-red");
      } else {
          factSpan.classList.add("highlight-green");
      }

      // Добавляем классы для планового значения
      // if (factValue >= planValue) {
      //     planSpan.classList.add("highlight-green");
      // } else {
      //     planSpan.classList.add("highlight-red");
      // }
  });
});