const cities = { "北海道": "016010", "青森県": "020010", "岩手県": "030010", "宮城県": "040010", "秋田県": "050010", "山形県": "060010", "福島県": "070010", "茨城県": "080010", "栃木県": "090010", "群馬県": "100010", "埼玉県": "110010", "千葉県": "120010", "東京都": "130010", "神奈川県": "1440010", "新潟県": "150010", "富山県": "160010", "石川県": "170010", "福井県": "180010", "山梨県": "190010", "長野県": "200010", "岐阜県": "210010", "静岡県": "220010", "愛知県": "230010", "三重県": "240010", "滋賀県": "250010", "京都府": "260010", "大阪府": "270000", "兵庫県": "280010", "奈良県": "290010", "和歌山県": "300010", "鳥取県": "310010", "島根県": "320010", "岡山県": "330010", "広島県": "340010", "山口県": "350010", "徳島県": "360010", "香川県": "370010", "愛媛県": "380010", "高知県": "390010", "福岡県": "400010", "佐賀県": "410010", "長崎県": "420010", "熊本県": "430010", "大分県": "440010", "宮崎県": "450010", "鹿児島県": "460010", "沖縄県": "470010", }
const element = (query) => document.querySelector(query)
const cL = (query) => element(query).classList
const on = (element, event, handler) => element.addEventListener(event, handler)

const historyPush = (href) => {
    history.pushState(href, href, href)
}

const backHome = () => {
    cL(".details").remove("active")
    cL(".home").add("active")
    historyPush("/")
}

const toDetails = (city) => {
    cL(".details").add("active")
    cL(".home").remove("active")
    historyPush(`/details?city=${city}`)
}

const renderDetails = (data) => {
    element(".prefecture").innerText = data.city
    element("img").src = data.image.url
    element(".max").innerText = data.weather.temperature.max || "情報がありませんでした"
    element(".min").innerText = data.weather.temperature.min || "情報がありませんでした"
}

on(element("button"), "click", async (e)=> {
    const value = element("select").value
    if(!value)
        return
    const res = await (await fetch(`/weather?city=${value}&id=${cities[value]}`)).json()
    toDetails(value)
    renderDetails(res)
})
on(element("a"), "click", async (e)=> {
    backHome()
})

const inti = async () => {
    if (location.pathname == "/details") {
        const value = (new URL(location.href)).searchParams.get("city")
        const res = await (await fetch(`/weather?city=${value}&id=${cities[value]}`)).json()
        toDetails(value)
        renderDetails(res)
        return
    }
    backHome()
}
inti()