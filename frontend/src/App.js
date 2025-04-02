import { createApp } from 'vue'
import { supabase } from './utils/supabaseClient'
import TaskForm from './components/TaskForm.vue'
import UserForm from './components/UserForm.vue'
import TaskList from './components/TaskList.vue'

const app = createApp({
    data() {
        return {
            tasks: [],
            users: [],
            showTaskForm: false,
            showUserForm: false
        }
    },
    async mounted() {
        await this.fetchData()
    },
    methods: {
        async fetchData() {
            const { data: tasks } = await supabase.from('tasks').select('*')
            const { data: users } = await supabase.from('users').select('*')
            this.tasks = tasks
            this.users = users
        },
        async handleAssign(taskId) {
            const response = await fetch(`/api/assign/${taskId}`, {
                method: 'POST'
            })
            if (response.ok) await this.fetchData()
        }
    },
    template: `
        <div class="container">
            <h1><img src="/assets/logo.svg" alt="Logo"> AI Task Allocator</h1>
            
            <div class="forms">
                <task-form @created="fetchData" v-if="showTaskForm"></task-form>
                <user-form @created="fetchData" v-if="showUserForm"></user-form>
                
                <button @click="showTaskForm = !showTaskForm">
                    {{ showTaskForm ? 'Cancel' : 'New Task' }}
                </button>
                <button @click="showUserForm = !showUserForm">
                    {{ showUserForm ? 'Cancel' : 'New User' }}
                </button>
            </div>

            <task-list :tasks="tasks" @assign="handleAssign"></task-list>
            
            <div class="team-view">
                <h2>Team Overview</h2>
                <div v-for="user in users" :key="user.id" class="user-card">
                    <h3>{{ user.name }}</h3>
                    <p>Skills: {{ user.skills }}</p>
                    <p>Capacity: {{ user.current_tasks?.length || 0 }}/{{ user.capacity }}</p>
                </div>
            </div>
        </div>
    `
})

app.component('TaskForm', TaskForm)
app.component('UserForm', UserForm)
app.component('TaskList', TaskList)
app.mount('#app')