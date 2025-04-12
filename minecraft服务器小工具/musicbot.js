const mineflayer = require('mineflayer');
const music = `

`;    //在这里粘贴
const bot = mineflayer.createBot({
    host: 'play.molean.com',
    port: 25565,
    username: 'hakoniwalily',
    password: '',
    auth: 'microsoft',
    version: "1.20.6"
});
start();
process.on("uncaughtException", (error) => {
    console.error(error);
});
function start() {
    bot.once('spawn', () => {
        const compose = music.trim().split('\n');
        let index = 0;
        const interval = setInterval(() => {
           bot.chat(compose[index]);
            index++;
            if (index >= compose.length) {
                clearInterval(interval);
                console.log("完成")
            }
    }, 1200);
    });
    bot.on('message', (jsonMsg) => {
        jsonMsg = jsonMsg.toString();
        console.log(jsonMsg);
    });
    bot.on("end", (reason) => {
        console.error("bot离线 : " + reason);
    });
    bot.on("error", (error) => {
        console.error(error.message);
    });
}