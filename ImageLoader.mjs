let imageDiv = document.getElementById("imageHolder");
/*
based on a list that i make manually, load all of those images, put them into imageHolder
with display: none; and then once document.all images are loaded or whatever the actual thing is
set allImagesLoaded to true (in main i guess?)
*/
export let allImagesLoaded = false;

// example part here, has to loop as well for things
let image = document.createElement("img");
image.style.display = "none";
image.src = imageSources[i];

imageDiv.appendChild(image)