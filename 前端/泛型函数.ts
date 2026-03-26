// 泛型函数：类型由调用时推断
function identity<T>(arg: T): T { return arg; }
identity<string>('hello');  // 显式指定
identity(42);               // 自动推断为 number

// 泛型约束（必须有 length 属性）
function getLength<T extends { length: number }>(arg: T): number {
  return arg.length;
}

// 泛型接口（API 响应通用类型）
interface ApiResponse<T> {
  code: number;
  data: T;
  message: string;
}
// 定义 User 接口
interface User {
  id: number;
  name: string;
}

const res: ApiResponse<User[]> = { code: 200, data: [], message: 'ok' };