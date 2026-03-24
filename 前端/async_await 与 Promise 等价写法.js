// ─── Promise 链式写法 ───
function getData() {
    return fetch('/api/user')
      .then(res => res.json())
      .then(user => fetch(`/api/orders/${user.id}`))
      .then(res => res.json())
      .catch(err => console.error(err));
  }
  
  // ─── 等价的 async/await 写法 ───
  async function getData() {
    try {
      const res1 = await fetch('/api/user');
      const user = await res1.json();
      const res2 = await fetch(`/api/orders/${user.id}`);
      return await res2.json();
    } catch (err) {
      console.error(err);
    }
  }
  
  // async 函数返回值永远是 Promise！
  async function foo() { return 42; }
  foo() instanceof Promise  // true
  foo().then(v => console.log(v))  // 42