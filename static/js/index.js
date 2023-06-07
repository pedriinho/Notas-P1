function confirmDeleteClassroom(event) {
    if(!confirm("Você tem certeza que deseja excluir?")){
        event.preventDefault();
    }
}