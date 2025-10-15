export const timeFormat = (sec: number | null): string => {
    if (!sec) return '00:00'
    let mathPrefix = sec < 0 ? '-' : ''
    sec = Math.abs(sec)
    let min = Math.trunc((sec % 3600) / 60)
    let minStr: string
    if (min < 10) minStr = `0${min}`
    else minStr = `${min}`
    return `${mathPrefix}${Math.trunc(sec / 3600)}:${minStr}`
}

export const numberFormat = (numb: number): string => {
    let parts = numb.toString().split('.')
    parts[0] = parts[0]!.replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    return parts.join('.')
}

export const percentFormat = (numb: number): string => {
    numb = Math.trunc(numb * 10000) / 100
    if (numb) return `${numb}%`
    else return '0 %'
}

export const strToCoord = (coord: string) => {
    return <TCoord>coord.split(', ').map(itm => parseFloat(itm))
}

export const monthByNum = (num: number) =>
    ({
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря',
    })[num]

export const dateToStr = (date: Date) => {
    let d = date.getDate()
    let dStr = d > 9 ? `${d}` : `0${d}`

    let m = date.getMonth() + 1
    let mStr = m > 9 ? `${m}` : `0${m}`

    return `${dStr}.${mStr}.${date.getFullYear()}`
}
