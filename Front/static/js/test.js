
const url = "http://127.0.0.1:3000/image"

async function upload() {
  let formData = new FormData();
  formData.append("file", fileupload.files[0]);
  await fetch(url, { method: "POST", body: formData })
    .then(response => {
      if (response.ok)
      console.log("SUCCESS")
      console.log(response.json())
    })
}