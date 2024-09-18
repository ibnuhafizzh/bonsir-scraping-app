document.addEventListener('DOMContentLoaded', function() {
    const addFieldButton = document.getElementById('add-field');
    const generateAndSortButton = document.getElementById('generate-and-sort'); // Combined button
    const inputFieldsDiv = document.getElementById('input-fields');
    const outputList = document.getElementById('output-list');

    function addNewField() {
        const newInputGroup = document.createElement('div');
        newInputGroup.className = 'input-group';
        
        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.name = 'input[]';
        newInput.placeholder = 'Enter text here';
        newInput.className = 'input-text';

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'X';
        deleteButton.className = 'delete-field';
        deleteButton.addEventListener('click', function() {
            inputFieldsDiv.removeChild(newInputGroup);
        });

        newInputGroup.appendChild(newInput);
        newInputGroup.appendChild(deleteButton);
        inputFieldsDiv.appendChild(newInputGroup);
    }

    async function generateAndSortList() {
        const items = Array.from(document.querySelectorAll('input[name="input[]"]'))
            .map(input => input.value.trim())
            .filter(value => value !== '');

        // Generate list
        outputList.innerHTML = '';
        items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = item;
            outputList.appendChild(listItem);
        });

        // Sort list
        const response = await fetch('/scraping-generator', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: items// Set to true if you want reverse order
            })
        });

        const data = await response.json();
        const sortedItems = data.sorted_items;

        // Clear the current list and display sorted items
        outputList.innerHTML = '';
        sortedItems.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = item;
            outputList.appendChild(listItem);
        });
    }

    addFieldButton.addEventListener('click', addNewField);
    generateAndSortButton.addEventListener('click', generateAndSortList); // Use combined button

    document.querySelectorAll('.delete-field').forEach(deleteButton => {
        deleteButton.addEventListener('click', function(event) {
            const inputGroup = event.target.parentElement;
            inputFieldsDiv.removeChild(inputGroup);
        });
    });
});