# Import the necessary libraries
import json

# Define the manifest for the Chrome extension
manifest = {
    "manifest_version": 3,
    "name": "My Chrome Extension",
    "version": "1.0",
    "permissions": ["downloads", "downloads.open"],
    "action": {
        "default_popup": "popup.html"
    },
    "background": {
        "service_worker": "background.js"
    },
    "icons": {
        "16": "icon.png",
        "48": "icon.png",
        "128": "icon.png"
    }
}

# Define the background JavaScript for the Chrome extension
background_js = """
self.oninstall = () => {
  self.onfetch = (event) => {
    if (event.request.url.includes('chrome-extension://')) {
      event.respondWith(fetch(event.request));
    }
  };
};
chrome.downloads.onDeterminingFilename.addListener(
  function(downloadItem, suggest) {
    suggest({filename: downloadItem.filename});
  });
"""

def main():
    # Write the manifest to manifest.json
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

    # Write the background JavaScript to background.js
    with open("background.js", "w") as f:
        f.write(background_js)

# Run the main function
if __name__ == "__main__":
    main()
