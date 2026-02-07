document.addEventListener("DOMContentLoaded", function () {

    const examSelect = document.getElementById("id_exam");
    const subjectSelect = document.getElementById("id_subject");

    if (!examSelect || !subjectSelect) return;

    examSelect.addEventListener("change", function () {
        const examId = this.value;

        subjectSelect.innerHTML = '<option value="">Loading...</option>';

        if (!examId) {
            subjectSelect.innerHTML = '<option value="">---------</option>';
            return;
        }

        fetch(`/exams/ajax/load-subjects/?exam_id=${examId}`)
            .then(response => response.json())
            .then(data => {
                subjectSelect.innerHTML = '<option value="">---------</option>';
                data.forEach(subject => {
                    const option = document.createElement("option");
                    option.value = subject.id;
                    option.textContent = subject.name;
                    subjectSelect.appendChild(option);
                });
            });
    });

});
