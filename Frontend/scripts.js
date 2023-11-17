function uploadFile() {
    // Filler script for the upload button
    alert("Upload functionality will be implemented here.");
  }
  
  function viewDocument() {
    // Filler script for the view button
    var documentName = document.getElementById("view").value;
    if (documentName.trim() !== "") {
      alert("Viewing document: " + documentName);
    } else {
      alert("Please enter a document hash.");
    }
  }