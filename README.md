<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Gmail API Integration with Python</h1>

<h2>Using Gmail API and Python to read email messages and download attachments</h2>

<p>Gmail API to be a bit confusing for beginners.</p>

<p>You have to set up your Google Cloud console to interact with the Gmail API.</p>
<p>
    Read <a href="https://www.geeksforgeeks.org/how-to-read-emails-from-gmail-using-gmail-api-in-python/">Geeksforgeeks</a> to 
    <a href="https://console.cloud.google.com/welcome?project=emailautomation-360404">Configure Google Cloud.</a>
    <div>
        <strong>"Error 403: access_denied"</strong> to fix this issue: <a href="https://stackoverflow.com/questions/65184355/error-403-access-denied-from-google-authentication-web-api-despite-google-acc">StackOverFlow</a>
    </div>

</p>

<h3>Therefore, I have created a Python script that does the following:</h3>
<ul>
    <li>Find and read all the unread messages.</li>
    <li>Extract details (Date, Sender, Subject, Snippet, Body) and export them to a .csv file / DB.</li>
    <li>Read attachments.</li>
    <li>Attachments write on csv file.</li>
</ul>


<h3>The script outputs a dictionary in the following format:</h3>

<div style="background-color: black; color:white">

{	
    'Sender': '"email.com" <name@email.com>', 
	'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
	'Date': 'yyyy-mm-dd', 
	'Message_body': 'Lorem ipsum dolor sit amet'
}

</div>

<p>The dictionary can be exported as a .csv or into a databse</p>

<div>
    Read documentaion for <a href="https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/index.html">more</a>
</div>

</body>
</html>
