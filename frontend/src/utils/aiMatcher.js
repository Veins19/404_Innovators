import { pipeline } from '@xenova/transformers'

export class TaskMatcher {
    static instance = null
    
    static async getInstance() {
        if (!this.instance) {
            this.instance = await pipeline(
                'feature-extraction',
                'Xenova/all-MiniLM-L6-v2'
            )
        }
        return this.instance
    }

    static async calculateSimilarity(text1, text2) {
        const extractor = await this.getInstance()
        const output1 = await extractor(text1, { pooling: 'mean', normalize: true })
        const output2 = await extractor(text2, { pooling: 'mean', normalize: true })
        return this.cosineSimilarity(output1.data, output2.data)
    }

    static cosineSimilarity(a, b) {
        const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0)
        const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0))
        const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0))
        return dotProduct / (magnitudeA * magnitudeB)
    }
}