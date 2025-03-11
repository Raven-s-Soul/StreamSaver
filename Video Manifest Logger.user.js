// ==UserScript==
// @name         Video Manifest Logger
// @namespace    http://tampermonkey.net/
// @version      2025-03-09
// @description  Log video manifest URL
// @author       none
// @match        *://*/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=sharepoint.com
// @grant       GM_notification
// @grant       GM_setClipboard
// ==/UserScript==

(function() {
    'use strict';

    console.log("Tampermonkey script is running!");

    // Function to copy text to clipboard
    function copyToClipboard(text) {
        GM_setClipboard(text, 'text');
    }

    function observeNetworkRequests() {
        if (window.performance && window.performance.getEntriesByType) {
            const resourceEntries = performance.getEntriesByType('resource');
            console.log("Resource Entries: ", resourceEntries);

            // Look for videomanifest requests
            resourceEntries.forEach((entry) => {
                if (entry.name.includes('videomanifest?provider')) {
                    let cleanUrl = entry.name.split('&altManifestMetadata')[0];
                    console.log('Found video manifest URL:', cleanUrl);
                    copyToClipboard(cleanUrl);
                    GM_notification ( { title: 'Found the manifest!', text: 'Now Paste'} );
                    return;
                }
            });
        }
    }

    window.addEventListener('load', observeNetworkRequests);
})();