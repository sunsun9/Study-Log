// 深拷贝&浅拷贝的区别：本质在于拷贝到嵌套对象时，是复制一份新的还是共用一个引用
// 前者是复制一个新的，后者则是只复制第一层，其他还是共用一个引用
// 因此，深拷贝后修改是不影响原数据的，而浅拷贝后修改是可能影响原对象的（第一层不影响，其他影响）。

// 手写深拷贝（支持循环引用，面试版）
function deepClone(obj, map = new WeakMap()) {
  // obj表示要克隆的对象，map记录已经克隆的对象

    // 为空或者基础类型->直接返回
    // 这是因为在JS中，基础类型指按值传递的，而不是引用
  if (obj === null || typeof obj !== 'object') return obj;  
  if (map.has(obj)) return map.get(obj);   // 处理循环引用，如果已经存在就直接返回
  if (obj instanceof Date)   return new Date(obj);
  if (obj instanceof RegExp) return new RegExp(obj);

  // 创建克隆容器，根据obj类型判断，保证克隆类型一致
  const clone = Array.isArray(obj) ? [] : {};
  map.set(obj, clone);    // 放入记录中
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      clone[key] = deepClone(obj[key], map);
    }
  }
  return clone;
}

// 现代项目首选（原生支持）
const copy = structuredClone(original);

function deepClone2(obj, map = new WeakMap()){
  if (obj === null || obj === 'object') return obj;
  if (map.has(obj)) return obj;
  if (obj instanceof Data) return new Date(obj);
  if (obj instanceof RegExp) return new RegExp(obj);

  const clone = Array.isArray(obj) ? [] : {};
  map.set(obj, clone);
  for (const key in obj){
    if (Object.prototype.hasOwnProperty.call(obj, key)){
      clone = deepClone2(obj[key], map);
    }
  }
  return clone;
}