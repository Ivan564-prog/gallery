const initImagePreview = () => {
    const imageFields = document.querySelectorAll('.field-image')
    
    imageFields.forEach(imageField => {
        const link = imageField.querySelector('a')
        if (!link)
            return
        const url = link['href']
        imageField.children[0].children[0].insertAdjacentHTML('beforeend', `<img src=${url} style="width: 60px; height: 60px; object-fit: contain;">`)
    })
}

document.addEventListener('DOMContentLoaded', () => {
    initImagePreview()
})