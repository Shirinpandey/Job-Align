const saveButtons = document.querySelectorAll('.btn-secondary');
const applysort = Array.from(document.getElementsByClassName('sort-button-apply'));
const form = document.querySelector('.sort-dropdown'); // This should be the <select> element
const jobCards = Array.from(document.querySelectorAll('.job-card'));
const jobGrid = document.querySelector('.jobs-grid'); // You need this for sorting display

// Centralized filter function
function filter(cards, attribute, filterValue) {
    const lowercaseFilter = (filterValue || '').toLowerCase();

    cards.forEach(card => {
        const cardAttributeValue = card.dataset[attribute];
        if (cardAttributeValue) {
            const lowercaseCardValue = cardAttributeValue.toLowerCase();
            card.style.display = lowercaseCardValue.includes(lowercaseFilter) ? '' : 'none';
        } else {
            card.style.display = 'none';
        }
    });
}

applysort.forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        const selectedOption = form.value;

        if (selectedOption === 'Sort by Match Score') {
            const sorted = [...jobCards].sort((a, b) => {
                return Number(b.dataset.score) - Number(a.dataset.score);
            });
            jobGrid.innerHTML = '';
            sorted.forEach(card => jobGrid.appendChild(card));
        }

        else if (selectedOption === 'Filter by Company') {
            const company = prompt('Enter Company Name:');
            if (company) filter(jobCards, 'company', company);
        }

        else if (selectedOption === 'Filter by Skill') {
            const skill = prompt('Enter Skill:');
            if (skill) filter(jobCards, 'skill', skill);
        }

        else if (selectedOption === 'Filter by Location') {
            const location = prompt('Enter Location:');
            if (location) filter(jobCards, 'location', location);
        }

        else if (selectedOption === 'Filter by Job Title') {
            const title = prompt('Enter Job Title:');
            if (title) filter(jobCards, 'title', title);
        }
    });
});

// Save/Remove Button Functionality
saveButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();

        const jobId = button.getAttribute('data_id');
        const action = button.getAttribute('action_needed');

        fetch('http://127.0.0.1:5000/search/save-job', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_id: jobId, action: action })
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    console.error("Server error (not JSON):", text);
                    throw new Error(`Server returned status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            if (action === 'remove') {
                const jobCard = button.closest('.job-card');
                if (jobCard) jobCard.remove();

                if (jobGrid && jobGrid.children.length === 0) {
                    const noJobsMessage = document.createElement('h3');
                    noJobsMessage.className = 'nojobs';
                    noJobsMessage.textContent = 'You have no saved jobs, browse to add!!';
                    jobGrid.appendChild(noJobsMessage);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error saving the job.');
        });
    });
});
