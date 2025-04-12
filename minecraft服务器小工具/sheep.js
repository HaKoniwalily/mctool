const { createBot } = require("mineflayer");
const { Vec3 } = require('vec3')

let username
let password
let level
let target_score

try {
    username = process.argv[2]                  //账号
    password = process.argv[3]                  //密码
    level = Number(process.argv[4])             //绵羊命坐数
    target_score = Number(process.argv[5])      //期望概率,最高75
    if (Number.isNaN(level) || Number.isNaN(target_score)) throw new Error()
} catch {
    console.log('参数错误！')
    process.exit()
}
main()
function main() {
    const bot = createBot({
        host: "play.molean.com",
        port: 25565,
        auth: 'microsoft',
        username,
       // password,
        version: "1.20.6"
    })
    function FF() {
        bot._client.write('block_dig', {
            status: 6,
            location: new Vec3(0, 0, 0),
            face: 0
        })
        setTimeout(_ => {
            bot._client.write('block_dig', {
                status: 6,
                location: new Vec3(0, 0, 0),
                face: 0
            })
        }, 50)
    }
    bot.once('spawn', _ => {
        bot.chat("/neeko use SHEEP")
        // console.log(bot);
        setTimeout(FF, 5000)
    })
    bot.on('end', reason => {
        console.log('自动重连30秒后启动');
        setTimeout(main, 30000)
    })
    bot.on('message', jsonMsg => {
        if (jsonMsg.text != '§8[§3温馨提示§8]') return
         msg = jsonMsg.toString()
        console.log(msg)
        try {
            const text = jsonMsg.extra[0].extra[1].text
            // console.log(text);
            const text_color = text.slice(1, text.length - 1).split(',')
            const color = new Vec3(Number(text_color[0]), Number(text_color[1]), Number(text_color[2]))
            const [score, best_color] = find_best(color)
            // console.log(score, best_color);
            if (score >= target_score) {
                console.log(`已找到最佳幸运色:${best_color.name}`)
                process.exit()
            }
            else setTimeout(FF, 50)
        } catch { }
    })
}
/**
 * 
 * @param {Vec3} color 
 * @returns
 */
function find_best(color) {
    let best_color = null
    let min_distance = 75
    let score = 0.0
    for (const i in Colors) {
        const sheep_color = Colors[i]
        const R = Math.floor(sheep_color.color / 65536)
        const G = Math.floor((sheep_color.color % 65536) / 256)
        const B = Math.floor(sheep_color.color % 256)
        const Color = color.offset(-R, -G, -B).abs()
        const distance = Color.x + Color.y + Color.z
        if (distance < min_distance) {
            min_distance = distance
            best_color = sheep_color
        }
    }
    switch (true) {
        case level < 3:
            score = (50 - min_distance) * 1.0
            break
        case level < 5:
            score = (50 - min_distance) * 1.5
            break
        default:
            score = (75 - min_distance) * 1.0
            break
    }
    return [score, best_color]
}

const Colors = [
    {
        color: 0xF9FFFE,
        name: "白色"
    },
    {
        color: 0xF9801D,
        name: "橙色"
    },
    {
        color: 0xC74EBD,
        name: "品红色"
    },
    {
        color: 0x3AB3DA,
        name: "淡蓝色"
    },
    {
        color: 0xFED83D,
        name: "黄色"
    },
    {
        color: 0x80C71F,
        name: "黄绿色"
    },
    {
        color: 0xF38BAA,
        name: "粉红色"
    },
    {
        color: 0x474F52,
        name: "灰色"
    },
    {
        color: 0x9D9D97,
        name: "淡灰色"
    },
    {
        color: 0x169C9C,
        name: "青色"
    },
    {
        color: 0x8932B8,
        name: "紫色"
    },
    {
        color: 0x3C44AA,
        name: "蓝色"
    },
    {
        color: 0x835432,
        name: "棕色"
    },
    {
        color: 0x5E7C16,
        name: "绿色"
    },
    {
        color: 0xB02E26,
        name: "红色"
    },
    {
        color: 0x1D1D21,
        name: "黑色"
    }
]