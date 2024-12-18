document.getElementById("submitBtn").addEventListener("click", async () => {
    const input = document.getElementById("imageInput");
    if (!input.files[0]) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append("image", input.files[0]);

    try {
        const response = await fetch("/api/process", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        const textOutput = document.getElementById("outputText");
        const definitionsOutput = document.getElementById("outputDefinitions");

        if (data.success) {
            // Display extracted text
            textOutput.textContent = data.text;

            // Display word definitions
            definitionsOutput.innerHTML = ""; // Clear previous definitions
            const wordDefinitions = data.word_definitions;
            for (const [word, definitions] of Object.entries(wordDefinitions)) {
                const wordDiv = document.createElement("div");
                wordDiv.innerHTML = `<strong>${word}</strong>:<ul>${definitions
                    .map(def => `<li>${def}</li>`)
                    .join("")}</ul>`;
                definitionsOutput.appendChild(wordDiv);
            }
        } else {
            textOutput.textContent = `Error: ${data.error}`;
            definitionsOutput.innerHTML = "";
        }
    } catch (err) {
        document.getElementById("outputText").textContent = `Error: ${err.message}`;
        document.getElementById("outputDefinitions").innerHTML = "";
    }
});
