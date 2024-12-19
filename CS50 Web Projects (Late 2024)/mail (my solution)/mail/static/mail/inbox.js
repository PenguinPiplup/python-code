document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Added
  const compose_recipients = document.querySelector('#compose-recipients');
  const compose_subject = document.querySelector('#compose-subject');
  const compose_body = document.querySelector('#compose-body');
  const compose_submit = document.querySelector('#compose-submit');

  // Clear out composition fields
  compose_recipients.value = '';
  compose_subject.value = '';
  compose_body.value = '';

  // Added: Disable submit button until recipient and subject fields are filled up
  compose_submit.disabled = true;

  function toggle_submit() {
    if (compose_recipients.value.length > 0 && compose_subject.value.length > 0) {
      compose_submit.disabled = false;
    }
    else {
      compose_submit.disabled = true;
    }
  }
  compose_recipients.onkeyup = toggle_submit;
  compose_subject.onkeyup = toggle_submit;

  // Added: Ability to submit form
  document.querySelector('#compose-form').onsubmit = event => {
    fetch("emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: compose_recipients.value,
        subject: compose_subject.value,
        body: compose_body.value
      })
    })
    .then (response => response.json())
    .then (result => {console.log(result);})
    .catch(error => {
      console.log('Error:', error);
    });

    load_mailbox('sent');
    return false;
  }
}


function reply_email(result_id) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Introduce variables
  const compose_recipients = document.querySelector('#compose-recipients');
  const compose_subject = document.querySelector('#compose-subject');
  const compose_body = document.querySelector('#compose-body');
  const compose_submit = document.querySelector('#compose-submit');

  // Pre-populate form
  fetch(`emails/${result_id}`)
  .then (response => response.json())
  .then (result => {
    compose_recipients.value = `${result.sender}`;
    compose_subject.value = `Re: ${result.subject}`;
    compose_body.value = `On ${result.timestamp} ${result.sender} wrote: \n${result.body}`;
  })
  .catch(error => {
    console.log('Error:', error);
  });

  function toggle_submit() {
    if (compose_recipients.value.length > 0 && compose_subject.value.length > 0) {
      compose_submit.disabled = false;
    }
    else {
      compose_submit.disabled = true;
    }
  }
  compose_recipients.onkeyup = toggle_submit;
  compose_subject.onkeyup = toggle_submit;

  // Ability to submit form
  document.querySelector('#compose-form').onsubmit = event => {
    fetch("emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: compose_recipients.value,
        subject: compose_subject.value,
        body: compose_body.value
      })
    })
    .then (response => response.json())
    .then (result => {console.log(result);})
    .catch(error => {
      console.log('Error:', error);
    });

    load_mailbox('sent');
    return false;
  }
}


function archive_helper(result_id, archive_status) {
  fetch(`emails/${result_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archive_status
    })
  })
  load_mailbox('inbox')
}

function archive_email(result_id) {
  archive_helper(result_id, true)
}

function unarchive_email(result_id) {
  archive_helper(result_id, false)
}


function load_mailbox(mailbox) {
  
  // Helper functions
  function show_all_emails(all_emails) {
    for (let email of all_emails) {
      let single_email = document.createElement('div');
      single_email.className = "mainpage_email";
      if (email.read === true) {
        single_email.style.backgroundColor = "lightgray";
      }
      if (mailbox === 'sent') {
        single_email.innerHTML = `<b>To ${email.recipients.toString()}</b> &nbsp &nbsp 
                                  <span style="width:100%; text-align:center;">${email.subject}</span>
                                  <span style="float:right;">${email.timestamp}</span>`;
      }
      else {
        single_email.innerHTML = `<b>From ${email.sender}</b> &nbsp &nbsp 
                                  <span style="width:100%; text-align:center;">${email.subject}</span>
                                  <span style="float:right;">${email.timestamp}</span>`;
      }
      
      // Show content of email when email is clicked on
      single_email.addEventListener('click', () => {
        fetch(`emails/${email.id}`)
        .then (response => response.json())
        .then (result => show_email(single_email, result, mailbox))
        .catch(error => {
          console.log('Error:', error);
        });
      })
      emails_view.appendChild(single_email);
    }
  }

  function show_email (single_email, result, mailbox) {
    console.log(result)
    
    fetch(`emails/${result.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
    single_email.style.backgroundColor = "lightgray";

    if (mailbox === 'inbox') {
      var archive_html = `<button onclick=archive_email(${result.id})>Archive</button>`;
    }
    else if (mailbox === 'archive') {
      var archive_html = `<button onclick=unarchive_email(${result.id})>Unarchive</button>`;
    }
    else {
      var archive_html = "";
    }

    single_email.innerHTML = `<b>Sender: </b> ${result.sender} <br>
                              <b>Receivers: </b> ${result.recipients.toString()} <br>
                              <b>Subject: </b> ${result.subject} <br>
                              <b>Body: </b> <br> ${result.body.replace(/\n/g, "<br>")} <br>
                              <b>Time Sent: </b> ${result.timestamp} <br><br>
                              <button onclick=reply_email(${result.id})>Reply</button> ${archive_html}`;

  }

  // Show the mailbox and hide other views
  const emails_view = document.querySelector('#emails-view');
  emails_view.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`emails/${mailbox}`)
  .then (response => response.json())
  .then (result => show_all_emails(result))
}