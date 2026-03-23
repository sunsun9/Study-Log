/* 
利用事件冒泡，将子元素监听器注册到父元素，通过 event.target 判断实际触发元素。
注意：e.target是事件对象的只读属性，是无法修改的
*/

// 完整封装版（支持 CSS selector 匹配）
function delegate(parent, selector, eventType, handler) {
    // parent → 要绑定监听器的父元素（比如 <ul>）
    // selector → 想要响应事件的子元素选择器（比如 'li'）
    // eventType → 事件类型（比如 'click'）
    // handler → 事件触发时执行的回调函数
  parent.addEventListener(eventType, function(e) {
    let target = e.target;
    while (target && target !== parent) {
      if (target.matches(selector)) {
        handler.call(target, e);
        return;
      }
      target = target.parentElement;    // 当前不匹配选择器
    }
  });
}

// 使用
delegate(document.getElementById('list'), 'li', 'click', function(e) {
  console.log('点击了：', this.textContent);
});

// 面试精简版（直接写）
document.getElementById('list').addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    console.log(e.target.textContent);
  }
});

function delegate2(parent, selector, eventType, handler){
    parent.addEventListener(eventType, function(e){
        let target = e.target;
        while (target && target !== parent){
            if (target.matches(selector)){
                handler.call(target, e);
                return;
            }
            target = target.parentElement;
        }
    })
}

document.getElementById('list').addEventListener('click', (e) => {
    if (e.target.tagName === 'LI'){
        console.log(e.target.textContent);
    }
})