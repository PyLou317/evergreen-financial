'use_strict';


let spinnerTimeout;

export function showSpinner() {
    const pageData = document.querySelector('.page-content')
    const spinner = document.querySelector('.loader-div');
    if (spinner) {
        console.log('spinner loaded');
        spinner.style.display = 'flex';
        pageData.style.display = 'none';
    }
}


export function hideSpinner() {
    const pageData = document.querySelector('.page-content')
    const spinner = document.querySelector('.loader-div');
    setTimeout(() => {
        if (spinner) {
            spinner.style.display = 'none';
        }
        if (pageData) {
            pageData.style.display = 'block';
        }
    }, 1000);
}


export function forceHideSpinner() {
    const spinner = document.querySelector('.loader-div');
    if (spinner) {
        clearTimeout(spinnerTimeout);
        spinner.classList.add =('visually-hidden');
    }
}
