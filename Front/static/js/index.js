const url = "http://127.0.0.1:3000/image";
const width = 1920 * 2;
const height = 1080 * 2;
const origin = [0, height];
const interval = 50;
const circle = true;

async function upload() {
  let formData = new FormData();
  formData.append("file", fileupload.files[0]);
  await fetch(url, { method: "POST", body: formData })
    .then((response) => {
      return response.json().then((data) => {
        const frames = JSON.parse(data);
        if (response.ok) {
          document.getElementsByClassName("canvas-wrapper")[0].style.display = "block";
          document.getElementsByClassName("image-post")[0].style.display = "none";
          animate(frames);
        }
        return data;
      })
    })
}

async function animate(frames) {
  const canvas = document.getElementById("anim");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  var quit = false;
  sets_of_tips = create_empty_sets(frames[0].length);
  var factor = get_zoom_factor();
  while (!quit) {
    for (let frame of frames) {
      sets_of_tips = draw(frame, ctx, sets_of_tips, factor);
      await new Promise(r => setTimeout(r, interval));
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  }
}

function create_empty_sets(len) {
  sets_of_tips = []
  for (let i = 0; i < len; i++) {
    sets_of_tips.push([]);
  }
  return sets_of_tips;
}

function get_zoom_factor() {
  return 0.5;
}

function transform_y(y_coordinate) {
  return - y_coordinate + height;
}


function draw_vector(ctx, previous_real, previous_imag, current_real, current_imag) {
  ctx.beginPath();
  ctx.moveTo(previous_real, previous_imag);
  ctx.lineTo(current_real, current_imag);
  ctx.stroke();
}

function draw_circle(ctx, current_real, current_imag, mag) {
  ctx.beginPath();
  ctx.arc(current_real, current_imag, mag, 0, Math.PI * 2);
  ctx.moveTo(current_real, current_imag);
  ctx.stroke();
}

function draw_path(ctx, tips) {
  ctx.beginPath();
  var first = true;
  for (let tip of tips) {
    if (first) {
      first = false;
    } else {
      ctx.lineTo(tip[0], tip[1]);
      // draw a line from the previous point to the next point
    }
    // Prevents the line from the origin to the first point of the path to be drawn
    ctx.moveTo(tip[0], tip[1]);
    // Move to the next point
    ctx.stroke();
  }
}


function draw(frame, ctx, sets_of_tips, factor) {
  var index = 0;
  for (let set_of_vec_data of frame) {
    ctx.moveTo(origin[0], origin[1]);
    var current_real = 0;
    var current_imag = 0;
    for (let vec_data of set_of_vec_data) {
      var real = vec_data[0][0] * factor;
      var imag = vec_data[0][1] * factor;
      var mag = vec_data[1] * factor;
      if (circle) {
        draw_circle(ctx, current_real, transform_y(current_imag), mag);
      }
      previous_real = current_real
      previous_imag = current_imag
      current_real += real;
      current_imag += imag;
      draw_vector(ctx, previous_real, transform_y(previous_imag), current_real, transform_y(current_imag));
    }
    sets_of_tips[index].push([current_real, transform_y(current_imag)])
    draw_path(ctx, sets_of_tips[index]);
    index++;
  }
  return sets_of_tips;
}
