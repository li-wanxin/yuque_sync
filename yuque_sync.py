from flask import Flask, request, jsonify
import subprocess
from loadConfig.loadConfig import Config

app = Flask(__name__)
conf = Config('_config.json')
print('load config finish!')


@app.route(conf.data['api']['path'], methods=['POST'])
def handle_post():
    try:
        # 获取请求的JSON数据
        data = request.get_json()
        # 判断JSON数据是否包含"upgrade"
        if data and 'upgrade' in data:
            # 执行elog sync命令
            print("recv upgrade command")
            result = subprocess.run(['elog', 'sync', '-e', '.elog.env'], cwd=conf.data['hexo']['path'], check=True)
            output = result.stdout
            print(output)
            if '任务结束' in output:
                if '同步成功' in output:
                    reflashHexo()
                    return jsonify({'status': 'success', 'message': 'elog sync success'}), 200
                elif '没有需要同步的文档' in output:
                    return jsonify({'status': 'success', 'message': 'elog sync no need'}), 200
                else:
                    return jsonify({'status': 'failure', 'message': 'elog sync return failed'}), 200
            else:
                return jsonify({'status': 'failure', 'message': 'elog sync return failed'}), 200
        else:
            return jsonify({'status': 'failure', 'message': 'post command error'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def reflashHexo():
    subprocess.run(['hexo', 'clean'], cwd=conf.data['hexo']['path'], check=True)
    subprocess.run(['hexo', 'g'], cwd=conf.data['hexo']['path'], check=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=conf.data['api']['port'])
