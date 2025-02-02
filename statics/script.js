document.addEventListener("DOMContentLoaded", () => {
    const databaseSelector = document.getElementById("databaseSelector");
    const searchInput = document.getElementById("searchInput");
    const tipsList = document.getElementById("tipsList");
    const searchTips = document.getElementById("searchTips");

    // Подсказки для каждой базы данных
    const tips = {
        quote: [
            "Search by name: <strong>name albert</strong>",
            "Search by tag: <strong>tag life</strong>",
            "Search by multiple tags: <strong>tags life, live</strong>"
        ],
        author: [
            "Search by person: <strong>person Albert Einstein</strong>",
            "Search by description: <strong>description physicist</strong>"
        ]
    };

    // Функция для обновления подсказок
    const updateTips = () => {
        const selectedDatabase = databaseSelector.value;
        tipsList.innerHTML = tips[selectedDatabase]
            .map(tip => `<li>${tip}</li>`)
            .join("");
    };

    // Обновляем подсказки при изменении выбора базы данных
    databaseSelector.addEventListener("change", updateTips);

    // Показываем подсказки при фокусе на поисковой строке
    searchInput.addEventListener("focus", () => {
        searchTips.style.display = "block";
        updateTips();
    });

    // Скрываем подсказки при потере фокуса
    searchInput.addEventListener("blur", () => {
        searchTips.style.display = "none";
    });

    // Обработчик поиска
    document.getElementById("searchButton").addEventListener("click", async () => {
        const query = searchInput.value.trim();
        if (!query) {
            alert("Please enter a search term.");
            return;
        }

        const selectedDatabase = databaseSelector.value;

        try {
            const response = await fetch("/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query, database: selectedDatabase })
            });
            if (!response.ok) {
                throw new Error("Network response was not ok.");
            }
            const data = await response.json();
            displayResults(data, selectedDatabase);
        } catch (error) {
            console.error("Error fetching data:", error);
            alert("An error occurred while fetching data.");
        }
    });

    // Функция для отображения результатов
    function displayResults(data, database) {
        console.log("Полученные данные:", data); // Отладка

        const resultsContainer = document.getElementById("results");
        resultsContainer.innerHTML = "";

        if (!Array.isArray(data) || data.length === 0) {
            resultsContainer.innerHTML = "<p>No results found.</p>";
            return;
        }

        if (database === "quote") {
            // Отображение цитат
            data.forEach(quote => {
                const quoteElement = document.createElement("div");
                quoteElement.classList.add("quote");

                const quoteText = document.createElement("p");
                quoteText.textContent = quote.quote;
                quoteElement.appendChild(quoteText);

                const author = document.createElement("div");
                author.classList.add("author");
                author.textContent = `— ${quote.author.fullname}`;
                quoteElement.appendChild(author);

                if (quote.tags && quote.tags.length > 0) {
                    const tags = document.createElement("div");
                    tags.classList.add("tags");
                    tags.textContent = `Tags: ${quote.tags.join(", ")}`;
                    quoteElement.appendChild(tags);
                }

                resultsContainer.appendChild(quoteElement);
            });
        } else if (database === "author") {
            // Отображение авторов
            data.forEach(author => {
                const authorElement = document.createElement("div");
                authorElement.classList.add("author");

                const name = document.createElement("h2");
                name.textContent = `— ${author.name.name}`;
                authorElement.appendChild(name);

                const bornDate = document.createElement("b");
                bornDate.textContent = `Born: ${author.born_date} in ${author.born_location}`;
                authorElement.appendChild(bornDate);

                const description = document.createElement("p");
                description.textContent = author.description;
                authorElement.appendChild(description);

                resultsContainer.appendChild(authorElement);
            });
        }
    }
});