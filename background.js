// Import the fetch API, used for making HTTP requests
const fetch = require('isomorphic-fetch');
const fs = require('fs');

// Define the Zapier Webhook URL
const zapierWebhookUrl = 'https://hooks.zapier.com/hooks/catch/10523644/364g899/';

// Map to keep track of download IDs
const downloadIds = new Map();

// Function to upload file to the provided Zapier Webhook URL
async function uploadToZapierWebhook(file) {
  // Convert the file to base64
  const fileContent = await file.arrayBuffer().then(result => btoa(String.fromCharCode(...new Uint8Array(result))));

  // Save the pdf file locally
  fs.writeFile('downloaded.pdf', fileContent, 'base64', err => {
    if (err) console.error(err);
    else console.log('PDF saved successfully');
  });

  // Make a POST request to the Zapier Webhook URL with the file's content
  try {
    const response = await fetch(zapierWebhookUrl, {
      method: 'POST',
      body: JSON.stringify({ file: fileContent }),
    });
    console.log(response);
  } catch (error) {
    console.error(error);
  }
}

// Listen for changes in the downloads
chrome.downloads.onChanged.addListener(async function(downloadDelta) {
  // If the download is complete and the download ID exists in the map
  if (downloadDelta.state && downloadDelta.state.current === 'complete' && downloadIds.has(downloadDelta.id)) {
    // Read the downloaded file
    const file = await chrome.downloads.open(downloadDelta.filename.current);

    // Upload the file to the Zapier Webhook
    await uploadToZapierWebhook(file);

    // Remove the download ID from the map
    downloadIds.delete(downloadDelta.id);
  }
});

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // If the command is 'downloadUrls'
  if (request.command === 'downloadUrls') {
    // For each URL in the request
    request.urls.forEach(url => {
      // Download the URL and add the download ID to the map
      chrome.downloads.download({url: url}, downloadId => downloadIds.set(downloadId, url));
    });
  }
});
