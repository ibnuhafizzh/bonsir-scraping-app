document.addEventListener('DOMContentLoaded', function () {
    const addFieldButton = document.getElementById('add-field');
    const inputFieldsContainer = document.getElementById('input-fields');
    
    // Add new input field when "+" button is clicked
    addFieldButton.addEventListener('click', function (e) {
        e.preventDefault();

        const inputGroup = document.createElement('div');
        inputGroup.classList.add('input-group');
        
        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'company[]';  // Input name to be sent with form
        input.placeholder = 'Enter company name';
        input.classList.add('input-text');

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'X';
        deleteButton.classList.add('delete-field');
        
        // Append input and delete button to the input group
        inputGroup.appendChild(input);
        inputGroup.appendChild(deleteButton);

        // Append input group to the container
        inputFieldsContainer.appendChild(inputGroup);
    });

    // Delete input field when "X" button is clicked
    inputFieldsContainer.addEventListener('click', function (e) {
        if (e.target && e.target.matches('.delete-field')) {
            e.preventDefault();
            e.target.parentNode.remove();
        }
    });
});
