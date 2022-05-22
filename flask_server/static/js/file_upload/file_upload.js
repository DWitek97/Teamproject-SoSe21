function getFileSize(elem) {
    console.log(elem.files[0].size);

    document.cookie = 'filesize=' + elem.files[0].size;
    console.log(document.cookie)
}

function getListingName(elem) {
    document.cookie = 'listingName=' + document.getElementById("inputName").value;
    console.log(document.cookie)
}