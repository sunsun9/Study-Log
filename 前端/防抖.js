function debounce(fn, delay, immediate = false) {
  // fn表示被防抖的函数，delay表示等待时间，immediate表示是否需要先执行一次
  let timer = null;
  return function(...args) {
    const callNow = immediate && !timer;
    clearTimeout(timer);    //取消timer的回调（会自动释放该timer），因为timer里包含了执行函数，也就是.apply()
    timer = setTimeout(() => {
      timer = null;   //当时间到了之后就要取消掉这个timer
      if (!immediate) fn.apply(this, args);
    }, delay);
    if (callNow) fn.apply(this, args);
  };
}

// 使用：搜索框输入 300ms 后才发请求
const handleSearch = debounce((e) => {
  console.log('搜索：', e.target.value);
}, 300);
input.addEventListener('input', handleSearch);

/* 第一次触发：
timer = null（初始状态）
↓
callNow = immediate && !null = true   ← 此时 timer 还是 null
↓
clearTimeout(null)  // 没效果
↓
timer = setTimeout(...)  // timer 现在有值了，也就是这里其实只是设置了一个ID，只要执行了都会有ID，并且创建一个对应的timer
↓
if (callNow) → true → fn() 立即执行 ✅

delay 内第二次触发：
timer = 有值（上一步设置的）
↓
callNow = immediate && !timer = false  ← timer 有值，所以 false
↓
clearTimeout(timer)  // 把上一个 timer 清掉
↓
timer = setTimeout(...)  // 重新设置 timer
↓
if (callNow) → false → 不执行 ❌
*/

function debounce2(fn, delay, immediate){
  let timer =null;
  return function(...args){
    const tag = immediate && !timer;
    clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      if(!immediate) fn.apply(this,args);
    }, delay);
    if(tag) fn.apply(this,args);
  }
}