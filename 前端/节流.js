// 时间戳版：立即执行，停止触发后不再执行最后一次
// 也就是每次点击的时候，如果与上一次执行的间隔小于预设，那就不执行；当本次点击与上一次执行>=预设，就执行
//本质：距离上次执行，过了足够长的时间吗
function throttle(fn, interval) {
  let lastTime = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      fn.apply(this, args);
    }
  };
}

// 定时器版：延迟执行，停止触发后最后一次一定会执行
function throttleTimer(fn, interval) {
  let timer = null;
  return function(...args) {
    if (!timer) {
      timer = setTimeout(() => {
        timer = null;
        fn.apply(this, args);
      }, interval);
    }
  };
}

// 使用：滚动事件每 200ms 最多触发一次
window.addEventListener('scroll', throttle(() => {
  console.log('scroll', window.scrollY);
}, 200));

// 二者的区别就是，前者在首次点击的时候会立刻执行，而后者还是需要等timer设置的delay。
// 最后一次点击过后，前者可能会没有反应，后者还是会等待最后一个timer执行完。

function throttle2(delay, fn){
  let lastTime = 0;
  return function(...args){
    const now = new Date.now();
    if(now - lastTime >= delay){
      lastTime = now;
      fn.apply(this, args);
    } 
  }
}

function throttle3(fn, delay){
  let timer = null;
  return function(...args){
    if (!timer){
      timer = setTimeout(() => {
        timer = null;
        fn.apply(this, args)
      }, delay);
    }
  }
}