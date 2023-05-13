// Initialize pdf data
let pdfData = {
    urls: [],
    names: [],
    paths: [],
    namesToUrls: {},
    namesToPaths: {},
    namesToNames: {},
};

// Function main(), to perform operations on pdfData
function main() {
    // For example, we can add data to our structure
    pdfData.urls.push('http://example.com/file1.pdf');
    pdfData.names.push('file1');
    pdfData.paths.push('/path/to/file1.pdf');
    
    // We can also map names to urls, paths and other names
    pdfData.namesToUrls['file1'] = 'http://example.com/file1.pdf';
    pdfData.namesToPaths['file1'] = '/path/to/file1.pdf';
    pdfData.namesToNames['file1'] = 'file1';
    
    // Log the updated pdfData to console
    console.log(pdfData);
}

// Call the main function
main();
