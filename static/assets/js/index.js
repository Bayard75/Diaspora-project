function checked()
{
    let residence_checked = document.querySelectorAll('input[name=residence]:checked');
    let origine_checked = document.querySelectorAll('input[name=origine]:checked');

    let residence_list = []
    residence_checked.forEach((box) => {
        let name = box.getAttribute('data')
       residence_list.push({"id":box.id, "name":name})
      });
    
    let origine_list = []
    origine_checked.forEach((box) => {
        let name = box.getAttribute('data')
        let short_name = box.getAttribute('short-name')

        origine_list.push({"id":box.id, "name":name, "short_name": short_name})
       });

      let body = {residence : residence_list, origine: origine_list};
      let myHeaders = new Headers();
      myHeaders.append("Content-Type","application/json"); //Important or request.get_json() returns None 

      fetch('/home', {
              // Specify the method
              method: 'POST',
              // A JSON payload
              body: JSON.stringify(body),
              headers: myHeaders
            })
            .then(function (response) 
            { 
                return response.json();

            })
            .then(function (data)
            {
                let path = data['path']
                let link = document.getElementById('download')
                link.style.display = "block";  
                link.setAttribute('href', path)  
            })

}

function checkAll(card)
{
    let boxes= document.querySelectorAll(`input[name=${card}]`);
    document.getElementById('uncheckall').checked = false;
    boxes.forEach((box) => {
        box.checked = true;
    });
}
function uncheckAll(card)
{
    let boxes= document.querySelectorAll(`input[name=${card}]`);
    document.getElementById('checkall').checked = false;

    boxes.forEach((box) => {
        box.checked = false;
    });
}