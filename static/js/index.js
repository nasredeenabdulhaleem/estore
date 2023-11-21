/* eslint-disable no-unused-vars */

function toggleSideNav() {
    console.log('Toggling navigation')
    const sideNav = document.getElementById('sideNav');
    const main = document.querySelector('main');
    if (sideNav.style.display === 'none') {
      sideNav.style.display = 'flex';
      sideNav.style.flexDirection = 'column';
      sideNav.style.placeContent = 'center';
      main.style.marginLeft = '15vw'

    } else {
      sideNav.style.display = 'none';
      main.style.marginLeft = '0'
    }
  }
  
  function checkScreenWidth() {
    const mdBreakpoint = 768; // This is the md breakpoint in Tailwind CSS
    const sideNav = document.getElementById('sideNav');
    const main = document.getElementsByTagName('main');
    if (window.innerWidth >= mdBreakpoint) {
      sideNav.style.display = 'none';
      main.style.marginLeft = '15vw'
    }
  }
  
  // Call the function once to set the initial state
  checkScreenWidth();
  
  // Add the event listener for the resize event
  window.addEventListener('resize', checkScreenWidth);
  

  document.addEventListener('DOMContentLoaded', function () {
    // Set the delay before hiding the toast
    const delay = 5000; // 5 seconds
  
    // Get the toast container and alerts
    const toastContainer = document.getElementById('toastContainer');
    const newMailAlert = document.getElementById('newMailAlert');
    const messageSentAlert = document.getElementById('messageSentAlert');
  
    // Function to hide the toast after a delay
    function hideToast() {
      toastContainer.classList.add('hide-toast');
    }
  
    // Show the toast initially
    setTimeout(hideToast, delay);
  
    // Add click event listeners to hide the toast on click
    newMailAlert.addEventListener('click', hideToast);
    messageSentAlert.addEventListener('click', hideToast);
  });
  