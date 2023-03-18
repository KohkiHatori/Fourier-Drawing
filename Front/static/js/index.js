const url = "http://127.0.0.1:3000/image";
const width = $(window).width();
const height = $(window).height();
const origin = [0, height];
const interval = 1;
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
  const canvas1 = document.getElementById("anim");
  canvas1.width = width;
  canvas1.height = height;
  const ctx1 = canvas1.getContext("2d");
  const canvas2 = document.getElementById("path");
  canvas2.width = width;
  canvas2.height = height;
  const ctx2 = canvas2.getContext("2d");
  let quit = false;
  const factor = get_zoom_factor();
  var t = 0;
  var sets_of_previous = Array(Object.keys(sets_of_coeffs).length)
  while (!quit) {
    sets_of_previous = draw(t, ctx1, ctx2, factor, sets_of_coeffs, sets_of_previous);
    await new Promise(r => setTimeout(r, interval));
    ctx1.clearRect(0, 0, canvas1.width, canvas1.height);
    t += DT;
  }
}


function get_zoom_factor() {
  return 0.1;
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

function draw_path(ctx, current_real, current_imag, previous) {
  if (previous != undefined && previous.length == 2) {
    draw_vector(ctx, previous[0], previous[1], current_real, current_imag)
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


function draw(t, ctx1, ctx2, factor, sets_of_coeffs, sets_of_previous) {
  var index = 0;
  for (let coeffs of sets_of_coeffs) {
    ctx1.moveTo(origin[0], origin[1]);
    var current_real = 0;
    var current_imag = 0;
    var n = 0;
    for (let i = 0; i < Object.keys(coeffs).length; i++) {
      let vector = get_vector(coeffs[n], n, t);
      let real = vector[0] * factor;
      let imag = vector[1] * factor;
      let mag = abs(vector) * factor;
      if (circle) {
        draw_circle(ctx1, current_real, transform_y(current_imag), mag);
      }
      previous_real = current_real
      previous_imag = current_imag
      current_real += real;
      current_imag += imag;
      draw_vector(ctx1, previous_real, transform_y(previous_imag), current_real, transform_y(current_imag));
      if (i % 2 == 0) {
        n += i + 1;
      } else {
        n *= -1;
      }
    }
    draw_path(ctx2, current_real, transform_y(current_imag), sets_of_previous[index]);
    sets_of_previous[index] = [current_real, transform_y(current_imag)];
    index++;
  }
  return sets_of_previous;
}
