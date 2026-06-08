function debounce(fn, delay) {
    // 防抖 稳定后执行
    let timer = null;
    return function(...args) {
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
            fn.apply(this, args);
        }, delay)
    }
}

function throttlr(fn, interval){
    let last = 0;
    return function(...args){
        let now = Date.now();
        if (now - last > interval){
            last = now;
            fn.apply(this, args);
        }
    }
}

function deepClone(obj, map = new WeakMap()){
    if (obj === null || typeof obj !== 'object')
        return obj;

    if (map.has(obj)){
        return map.get(obj)
    }
    const clone = Array.isArray(obj) ? [] : {};
    map.set(obj, clone);
    
    for (const key in obj){
        if(Object.prototype.hasOwnProperty(key)){
            clone[key] = deepClone(obj[key], map);
        }
    }
    return clone;
}

function myPromiseAll(promises) {
    return new Promise((resolve, reject) => {
        
        // 边界处理
        if (!Array.isArray(promises)) {
            return reject(new TypeError("参数必须是数组"));
        }
        
        if (promises.length === 0) {
            return resolve([]);
        }

        const results = [];
        let completedCount = 0;

        promises.forEach((promise, index) => {
            // 用 Promise.resolve 包一下，兼容传入非Promise的值
            Promise.resolve(promise).then(value => {
                results[index] = value;        // 按原始顺序存结果
                completedCount++;

                if (completedCount === promises.length) {
                    resolve(results);          // 全部完成才 resolve
                }
            }).catch(err => {
                reject(err);                   // 任何一个失败立即 reject
            });
        });
    });
}