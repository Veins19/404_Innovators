const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_KEY = 'your-anon-key';

// Initialize Supabase client
const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

async function createTask(taskData) {
    const { data, error } = await supabase
        .from('tasks')
        .insert([taskData]);
    
    if (error) console.error(error);
    else console.log('Task created:', data);
}