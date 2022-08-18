let sidebar = document.querySelector(".sidebar");
  let closeBtn = document.querySelector("#btn");
  let analysisiconBtn = document.querySelector(".bx-pie-chart-alt-2");
  let analysisBtn = document.querySelector(".links_name2");
  let individualBtn = document.querySelector("#indi_g");
  let cumulativeBtn = document.querySelector("#cumu_g");
  let hoverBtn = document.querySelector(".hover_bkgr_fricc");
  let popupcloseBtn = document.querySelector(".popupCloseButton")

  closeBtn.addEventListener("click", ()=>{
    sidebar.classList.toggle("open");
    menuBtnChange();//calling the function(optional)
  });

  analysisiconBtn.addEventListener("click", ()=>{ // Sidebar open when you click on the search iocn
    sidebar.classList.toggle("open");
    menuBtnChange(); //calling the function(optional)
  });

  // following are the code to change sidebar button(optional)
  function menuBtnChange() {
   if(sidebar.classList.contains("open")){
     closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
   }else {
     closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
   }
  }

  window.onload = (event) =>  {
    analysisBtn.addEventListener("click", () =>{
      hoverBtn.style.display = "block";
    });
    hoverBtn.addEventListener("click", () =>{
      hoverBtn.style.display = "none";
    });
    popupcloseBtn.addEventListener("click", () =>{
      hoverBtn.style.display = "none";
    });
};