import { supabase } from '../../../src/utils/supabaseClient'

export default async (req, res) => {
    const { taskId } = req.query
    
    try {
        // Get task details
        const { data: task, error: taskError } = await supabase
            .from('tasks')
            .select('*')
            .eq('id', taskId)
            .single()

        if (taskError) throw taskError

        // Get available users
        const { data: users, error: usersError } = await supabase
            .from('users')
            .select('*')
            .lte('current_tasks:length', 'capacity')

        if (usersError) throw usersError

        // Return data for client-side matching
        res.status(200).json({
            task,
            users,
            message: 'Ready for client-side AI matching'
        })
        
    } catch (error) {
        res.status(500).json({ error: error.message })
    }
}