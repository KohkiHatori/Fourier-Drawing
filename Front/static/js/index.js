const url = "http://127.0.0.1:3000/image";
const width = 1920 * 2;
const height = 1080 * 2;
const origin = [0, height];
const interval = 10;
const circle = true;
const DT = 0.001;

async function upload() {
  let formData = new FormData();
  formData.append("file", fileupload.files[0]);
  await fetch(url, { method: "POST", body: formData })
    .then((response) => {
      return response.json().then((data) => {
        const sets_of_coeffs = JSON.parse(data);
        if (response.ok) {
          document.getElementsByClassName("canvas-wrapper")[0].style.display = "block";
          document.getElementsByClassName("image-post")[0].style.display = "none";
          animate(sets_of_coeffs);
        }
        return data;
      })
    })
}

async function animate(sets_of_coeffs) {
  console.log(sets_of_coeffs[0])
  const canvas = document.getElementById("anim");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  let quit = false;
  var sets_of_tips = create_empty_sets(Object.keys(sets_of_coeffs).length);
  const factor = get_zoom_factor();
  var t = 0;
  console.log(sets_of_coeffs[0]);
  while (!quit) {
    sets_of_tips = draw(t, ctx, sets_of_tips, factor, sets_of_coeffs);
    await new Promise(r => setTimeout(r, interval));
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    t += DT;
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

function get_vector(coeff, n, t) {
  let coeff_real = coeff[0];
  let coeff_imag = coeff[1];
  let e_real = Math.cos(2 * Math.PI * n * t);
  let e_imag = Math.sin(2 * Math.PI * n * t);
  let vector_real = coeff_real * e_real - coeff_imag * e_imag;
  let vector_imag = coeff_imag * e_real + coeff_real * e_imag;
  return [vector_real, vector_imag];
}

function abs(vector) {
  return Math.sqrt(vector[0] ** 2 + vector[1] ** 2);
}

function get_mags() {
  return 0;
}


function draw(t, ctx, sets_of_tips, factor, sets_of_coeffs) {
  var index = 0;
  for (let coeffs of sets_of_coeffs) {
    ctx.moveTo(origin[0], origin[1]);
    var current_real = 0;
    var current_imag = 0;
    var n = 0;
    for (let i = 0; i < Object.keys(coeffs).length; i++) {
      let vector = get_vector(coeffs[n], n, t);
      let real = vector[0] * factor;
      let imag = vector[1] * factor;
      let mag = abs(vector) * factor;
      if (circle) {
        draw_circle(ctx, current_real, transform_y(current_imag), mag);
      }
      previous_real = current_real
      previous_imag = current_imag
      current_real += real;
      current_imag += imag;
      draw_vector(ctx, previous_real, transform_y(previous_imag), current_real, transform_y(current_imag));
      if (i % 2 == 0) {
        n += i + 1;
      } else {
        n *= -1;
      }
    }
    sets_of_tips[index].push([current_real, transform_y(current_imag)])
    draw_path(ctx, sets_of_tips[index]);
    index++;
  }
  return sets_of_tips;
}
