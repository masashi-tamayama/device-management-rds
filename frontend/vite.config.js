import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react-swc';
import { resolve } from 'path';
// https://vitejs.dev/config/
export default defineConfig(function (_a) {
    var command = _a.command, mode = _a.mode;
    // 環境変数をロード
    var env = loadEnv(mode, process.cwd(), '');
    return {
        plugins: [react()],
        resolve: {
            alias: {
                '@': resolve(__dirname, './src')
            }
        },
        server: {
            port: 3000,
            open: true,
            cors: true
        },
        build: {
            outDir: 'dist',
            sourcemap: command === 'serve'
        }
    };
});
