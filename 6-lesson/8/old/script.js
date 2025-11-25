let likes1 = 0;
let likes2 = 0;
let likes3 = 0;
let lastPostId = 3;

document.getElementById("like-1").addEventListener("click", function () {
  likes1++;
  this.textContent = "Лайков: " + likes1;
});

document.getElementById("like-2").addEventListener("click", function () {
  likes2++;
  this.textContent = "Лайков: " + likes2;
});

document.getElementById("like-3").addEventListener("click", function () {
  likes3++;
  this.textContent = "Лайков: " + likes3;
});

document.getElementById("delete-1").addEventListener("click", function () {
  document.getElementById("post-1").remove();
});

document.getElementById("delete-2").addEventListener("click", function () {
  document.getElementById("post-2").remove();
});

document.getElementById("delete-3").addEventListener("click", function () {
  document.getElementById("post-3").remove();
});

document.getElementById("add-post").addEventListener("click", function () {
  lastPostId++;
  const id = lastPostId;

  const container = document.createElement("div");
  container.className = "post";
  container.id = "post-" + id;
  container.innerHTML = `
    <h2>Пост ${id}</h2>
    <p>Текст поста ${id}</p>
    <button id="like-${id}">Лайков: 0</button>
    <button id="delete-${id}">Удалить</button>
  `;

  document.body.insertBefore(
    container,
    document.getElementById("add-post")
  );

  let likes = 0;

  const likeButton = document.getElementById("like-" + id);
  const deleteButton = document.getElementById("delete-" + id);

  likeButton.addEventListener("click", function () {
    likes++;
    likeButton.textContent = "Лайков: " + likes;
  });

  deleteButton.addEventListener("click", function () {
    container.remove();
  });
});
