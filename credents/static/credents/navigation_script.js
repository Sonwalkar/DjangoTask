const togglebutton = document.getElementsByClassName('toggle-button')[0]
const navbarlinks =document.getElementsByClassName('navlinks')[0]

togglebutton.addEventListener('click',() => {
    navbarlinks.classList.toggle('active')
})