from mvc.controllers.activities_list_controller import ActivitiesListController
from mvc.controllers.activity_form_controller import ActivityFormController
from mvc.controllers.create_account_controller import CreateAccountController
from mvc.controllers.home_controller import HomeController
from mvc.controllers.login_controller import LoginController
from mvc.views.activities_list_view import ActivitiesListView
from mvc.views.activity_form_view import ActivityFormView
from mvc.views.create_account_view import CreateAccountView
from mvc.views.home_view import HomeView
from mvc.views.login_view import LoginView


class NavigationController:
    """Responsável por trocar as telas da janela principal."""

    def __init__(self, root):
        self.root      = root
        self._current  = None   # frame ativo no momento
        self._user     = None   # usuário logado, guardado para uso nas telas internas

    def _swap(self, view, title="DietTracker"):
        # Destrói a tela atual antes de exibir a nova e atualiza o título da janela
        if self._current:
            self._current.destroy()
        self._current = view
        self.root.title(title)
        view.pack(fill="both", expand=True)

    # ---- Login e cadastro ------------------------------------------------

    def show_login(self):
        view = LoginView(self.root)
        ctrl = LoginController(view)
        view.on_submit         = ctrl.handle_submit
        view.on_create_account = self.show_create_account  # link "Criar conta"
        ctrl.on_success        = self.show_home            # login ok → painel
        self._swap(view)

    def show_create_account(self):
        view = CreateAccountView(self.root, on_cancel=self.show_login)
        ctrl = CreateAccountController(view)
        view.on_submit  = ctrl.handle_submit
        ctrl.on_success = self.show_login  # cadastro ok → redireciona para login
        self._swap(view)

    # ---- Painel principal ------------------------------------------------

    def show_home(self, user=None):
        # Armazena o usuário ao fazer login pela primeira vez;
        # nas chamadas subsequentes (ex: voltar de outra tela) reutiliza o mesmo usuário
        if user is not None:
            self._user = user

        view = HomeView(self.root, self._user, on_logout=self.show_login)
        ctrl = HomeController(view, self._user)

        # Registra os handlers de cada seção implementada
        # Seções ainda não implementadas cairão no "Em breve" do HomeController
        ctrl.on_navigate_to["activities"] = self.show_activities

        view.on_navigate = ctrl.handle_navigate
        self._swap(view, "DietTracker — Painel")

    # ---- Atividades físicas (UC06) ---------------------------------------

    def show_activities(self):
        view = ActivitiesListView(
            self.root,
            on_back = self.show_home,                          # "← Voltar" → painel
            on_new  = lambda: self.show_activity_form(),       # "+" → formulário vazio
            on_edit = lambda act: self.show_activity_form(act),# "Editar" → formulário preenchido
        )
        ctrl = ActivitiesListController(view, self._user)
        # Os callbacks de delete e filtro precisam do controller, por isso são atribuídos
        # separadamente (o controller ainda não existe quando a view é criada acima)
        view.on_delete      = ctrl.handle_delete
        view.on_date_change = ctrl.handle_date_change
        ctrl.load()  # carrega as atividades de hoje ao abrir a tela
        self._swap(view, "DietTracker — Atividades Físicas")

    def show_activity_form(self, activity=None):
        # activity=None → modo criação; activity=<objeto> → modo edição
        view = ActivityFormView(
            self.root,
            activity  = activity,
            on_cancel = self.show_activities,  # "Cancelar" / "← Voltar" → lista
        )
        ctrl = ActivityFormController(view, self._user, activity)
        view.on_submit = ctrl.handle_submit  # "Salvar atividade" → valida e persiste

        title = "DietTracker — Editar Atividade" if activity else "DietTracker — Nova Atividade"
        self._swap(view, title)
