import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json; charset=utf-8',
    'Accept-Language': 'ja',
  },
  timeout: 10000, // 10秒でタイムアウト
});

// リクエストインターセプター
apiClient.interceptors.request.use(
  (config) => {
    // リクエスト前の処理（必要に応じてトークンの追加など）
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// レスポンスインターセプター
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // サーバーからのエラーレスポンス
      switch (error.response.status) {
        case 400:
          console.error('バリデーションエラー:', error.response.data);
          break;
        case 401:
          console.error('認証エラー:', error.response.data);
          break;
        case 404:
          console.error('リソースが見つかりません:', error.response.data);
          break;
        case 500:
          console.error('サーバーエラー:', error.response.data);
          break;
        default:
          console.error('予期せぬエラー:', error.response.data);
      }
    } else if (error.request) {
      // リクエストは送信されたがレスポンスがない
      console.error('ネットワークエラー:', error.request);
    } else {
      // リクエストの作成時にエラーが発生
      console.error('リクエストエラー:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient; 