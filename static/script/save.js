const saveButtons = document.querySelectorAll('.btn-secondary');

saveButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        console.log('Save button clicked'); // Debugging line
        const jobId = button.getAttribute('data_id');
        const action = button.getAttribute('action_needed');
        console.log(`Job ID: ${jobId}, Action: ${action}`);
        
        fetch('http://127.0.0.1:5000/search/save-job', {  // Ensure the endpoint matches your Flask route
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_id: jobId, action: action })
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    console.error("Server error (not JSON):", text);
                    throw new Error(`Server returned non-OK response: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Response received:', data); // Debugging line
            alert(data.message);

            if (action === 'remove') {
                const jobCard = button.closest('.job-card');
                if (jobCard) {
                    jobCard.remove();
                }

                const jobGrid = document.querySelector('.jobs-grid');
                if (jobGrid && jobGrid.children.length === 0) {
                    const noJobsMessage = document.createElement('h3');
                    noJobsMessage.className = 'nojobs';
                    noJobsMessage.textContent = 'You have no saved jobs browse to add!!';
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
